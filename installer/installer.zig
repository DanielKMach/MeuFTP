const std = @import("std");
const builtin = @import("builtin");

var in: std.fs.File.Reader = undefined;
var out: std.fs.File.Writer = undefined;

var alloc: std.mem.Allocator = undefined;

pub fn main() !void {
    in = std.io.getStdIn().reader();
    out = std.io.getStdOut().writer();

    // Alocador de memória
    const malloc = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    alloc = malloc.child_allocator;
    defer malloc.deinit();

    defer {
        _ = out.write("Pressione [ENTER] para continuar...") catch void;
        _ = in.readByte() catch void;
    }

    const result = switch (builtin.os.tag) {
        .windows => install_windows(),
        .linux => install_linux(),

        else => install_unknown(),
    };

    if (result) |_| {
        _ = try out.write("MeuFTP instalado!\n");
    } else |err| {
        _ = switch (err) {
            error.AccessDenied => try out.write("O instalador não tem permissão para instalar MeuFTP.\n"),
            error.BadPathName => try out.write("Não foi possível encontrar um local de instalação no seu dispositivo.\n"),
            else => try out.write("Não foi possível instalar MeuFTP no seu dispositivo.\n"),
        };
    }
}

fn install_windows() anyerror!void {
    _ = try out.write("Instalando MeuFTP para Windows...\n");

    const path = "C:\\Windows\\";
    const file_name = "meuftp.cmd";

    // Criando o caminho do arquivo
    var dir = try std.fs.openDirAbsolute(path, .{});
    defer dir.close();

    // Criando e acessando o arquivo
    var file = try dir.createFile(file_name, .{});
    defer file.close();

    // Escrevendo para o arquivo
    const content = try std.fmt.allocPrint(alloc, "@echo off\n\npython \"{s}\\src\\meuftp.py\"", .{try std.fs.cwd().realpathAlloc(alloc, ".")});
    _ = try file.writeAll(content);

    // Adicionando ao PATH
    // TODO
}

fn install_linux() anyerror!void {
    _ = try out.write("Instalando MeuFTP para Linux...\n");

    const path = "~/home/bin/";
    const file_name = "meuftp";

    // Criando e acessando o arquivo
    var dir = try std.fs.openDirAbsolute(path, .{});
    defer dir.close();

    var file = try dir.createFile(file_name, .{});
    defer file.close();

    // Escrevendo para o arquivo
    const content = try std.fmt.allocPrint(alloc, "#!/bin/bash\n\npython3 \"{s}/src/meuftp.py\"", .{try std.fs.cwd().realpathAlloc(alloc, ".")});
    _ = try file.writeAll(content, .{});
}

fn install_unknown() anyerror!void {
    _ = try out.write("Este sistema operacional não é suportado pelo MeuFTP.");
}
