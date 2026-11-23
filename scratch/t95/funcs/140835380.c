__int64 __fastcall sub_140835380(__int64 *a1, int a2, __int64 *a3)
{
  __int64 result; // rax
  __int64 v7; // rbx
  __int64 v8; // rcx
  __int64 *v9; // rdi
  __int64 v10; // rax
  __int64 v11; // rcx
  __int64 v12; // rcx
  __int64 v13; // rdi
  __int64 v14; // rax
  _QWORD *v15; // rsi
  __int64 v16; // rax
  __int64 v17; // rcx
  int v18; // [rsp+2Ch] [rbp-4h] BYREF
  __int64 v19; // [rsp+30h] [rbp+0h]

  v19 = -2;
  result = *a1;
  v7 = a1[1];
  if ( *a1 == v7 )
    goto LABEL_10;
  v8 = *a1;
  while ( *(_DWORD *)v8 != a2 )
  {
    v8 += 16;
    if ( v8 == v7 )
      goto LABEL_10;
  }
  if ( v8 == v7 || (v9 = *(__int64 **)(v8 + 8)) == nullptr )
  {
LABEL_10:
    v18 = a2;
    v12 = a1[2];
    if ( v12 == result )
    {
      sub_140837DD0(a1, 4);
      v7 = a1[1];
      if ( v7 != a1[2] )
      {
LABEL_12:
        *(_DWORD *)v7 = a2;
        v13 = sub_140836BC0();
        v14 = MEMORY[0x1419475D0](v13 + 32);
        v15 = (_QWORD *)v14;
        if ( v14 != 0 && *(_BYTE *)(v13 + 72) != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v13 + 64));
        if ( v14 == 0 )
          v15 = (_QWORD *)sub_1412D31C0(
                            v13,
                            *(unsigned int *)(v13 + 80),
                            *(unsigned int *)(v13 + 4LL * (*(_DWORD *)(v13 + 56) != 0) + 84));
        if ( v15 != nullptr && *(_BYTE *)(v13 + 96) != 0 )
          sub_141758A10(v15, 0, *(unsigned int *)(v13 + 80));
        v16 = *a3;
        v17 = a3[1];
        v15[1] = v17;
        *v15 = v16;
        result = sub_14083D4F0(v17) + 8;
        a3[1] = 0;
        *a3 = result;
        *(_QWORD *)(v7 + 8) = v15;
        a1[1] += 16;
        return result;
      }
    }
    else if ( v7 != v12 )
    {
      goto LABEL_12;
    }
    return sub_140837870(a1, v7, &v18, a3);
  }
  if ( v9 != a3 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v9 + 16LL))(*v9, v9);
    v10 = *a3;
    v11 = a3[1];
    v9[1] = v11;
    *v9 = v10;
    result = sub_14083D4F0(v11) + 8;
    a3[1] = 0;
    *a3 = result;
  }
  return result;
}
