// THUNK ALIAS -> sub_143774BA0 (jmp:0x140835a40->0x143774ba0)
__int64 __fastcall sub_143774BA0(_QWORD *a1, int a2, _QWORD *a3)
{
  __int64 v6; // rdx
  __int64 v7; // r15
  __int64 v8; // rbx
  __int64 v9; // rax
  __int64 v10; // rdi
  int v12; // [rsp+2Ch] [rbp-4h] BYREF
  __int64 v13; // [rsp+30h] [rbp+0h]

  v13 = -2;
  v12 = a2;
  v6 = a1[2];
  if ( v6 == *a1 )
  {
    sub_140837DD0(a1, 4);
    v6 = a1[2];
  }
  v7 = a1[1];
  if ( v7 == v6 )
    return sub_140837510(a1, v6, &v12, a3);
  *(_DWORD *)v7 = a2;
  v8 = sub_140836BC0();
  v9 = MEMORY[0x1419475D0](v8 + 32);
  v10 = v9;
  if ( v9 != 0 && *(_BYTE *)(v8 + 72) != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v8 + 64));
  if ( v9 == 0 )
    v10 = sub_1412D31C0(v8, *(unsigned int *)(v8 + 80), *(unsigned int *)(v8 + 4LL * (*(_DWORD *)(v8 + 56) != 0) + 84));
  if ( v10 != 0 && *(_BYTE *)(v8 + 96) != 0 )
    sub_141758A10(v10, 0, *(unsigned int *)(v8 + 80));
  (*(void (__fastcall **)(_QWORD, _QWORD *, __int64))(*(_QWORD *)*a3 + 24LL))(*a3, a3, v10);
  *(_QWORD *)(v7 + 8) = v10;
  a1[1] += 16LL;
  return v10;
}
