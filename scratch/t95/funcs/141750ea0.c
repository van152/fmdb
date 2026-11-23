// THUNK ALIAS -> sub_1447C4E60 (jmp:0x141750ea0->0x1447c4e60)
__int64 __fastcall sub_1447C4E60(_DWORD *a1)
{
  __int64 v2; // rdx

  MEMORY[0x141947418](&unk_141AC5D28);
  v2 = (unsigned int)TlsIndex;
  *a1 = ++dword_141A8F920;
  *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + v2) + 4LL) = dword_141A8F920;
  MEMORY[0x141947608](&unk_141AC5D28);
  return sub_141750F64();
}
