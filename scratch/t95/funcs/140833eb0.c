__int64 __fastcall sub_140833EB0(_QWORD *a1, int a2, __int64 *a3)
{
  __int64 v6; // rdx
  __int64 v7; // r15
  __int64 v8; // rsi
  __int64 v9; // rax
  _QWORD *v10; // rbx
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 result; // rax
  int v14; // [rsp+2Ch] [rbp-4h] BYREF
  __int64 v15; // [rsp+30h] [rbp+0h]

  v15 = -2;
  v14 = a2;
  v6 = a1[2];
  if ( v6 == *a1 )
  {
    sub_140837DD0(a1, 4);
    v6 = a1[2];
  }
  v7 = a1[1];
  if ( v7 == v6 )
    return sub_140837870(a1, v6, &v14, a3);
  *(_DWORD *)v7 = a2;
  v8 = sub_140836BC0();
  v9 = MEMORY[0x1419475D0](v8 + 32);
  v10 = (_QWORD *)v9;
  if ( v9 != 0 && *(_BYTE *)(v8 + 72) != 0 )
    _InterlockedIncrement((volatile signed __int32 *)(v8 + 64));
  if ( v9 == 0 )
    v10 = (_QWORD *)sub_1412D31C0(
                      v8,
                      *(unsigned int *)(v8 + 80),
                      *(unsigned int *)(v8 + 4LL * (*(_DWORD *)(v8 + 56) != 0) + 84));
  if ( v10 != nullptr && *(_BYTE *)(v8 + 96) != 0 )
    sub_141758A10(v10, 0, *(unsigned int *)(v8 + 80));
  v11 = *a3;
  v12 = a3[1];
  v10[1] = v12;
  *v10 = v11;
  result = sub_14083D4F0(v12) + 8;
  a3[1] = 0;
  *a3 = result;
  *(_QWORD *)(v7 + 8) = v10;
  a1[1] += 16LL;
  return result;
}
