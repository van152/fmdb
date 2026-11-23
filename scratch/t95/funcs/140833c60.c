_QWORD *__fastcall sub_140833C60(_QWORD *a1, int a2, _QWORD *a3)
{
  _QWORD *v5; // rcx
  __int64 v6; // rsi
  __int64 v7; // rdi
  __int64 v8; // rax
  _QWORD *v9; // rbx
  _QWORD *v10; // rdi
  __int64 v11; // rax
  __int64 v12; // rcx
  __int64 v13; // rax
  int v15; // [rsp+2Ch] [rbp-14h] BYREF
  _QWORD *v16; // [rsp+30h] [rbp-10h]
  _QWORD *v17; // [rsp+38h] [rbp-8h]
  __int64 v18; // [rsp+40h] [rbp+0h]

  v18 = -2;
  v17 = a3;
  if ( qword_141ABD470 == 0 )
  {
    if ( dword_141B59AA8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                     + 4LL) )
    {
      sub_141750E08(&dword_141B59AA8);
      if ( dword_141B59AA8 == -1 )
      {
        sub_1407E3E70(&unk_141B59A68);
        sub_141751048(sub_1407E4B20);
        sub_141750EA0(&dword_141B59AA8);
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  a1[2] = 0;
  a1[1] = 0;
  *a1 = 0;
  v15 = a2;
  v16 = a1;
  sub_140837DD0(a1, 4);
  v5 = a1;
  v6 = a1[1];
  if ( v6 == v5[2] )
  {
    sub_140837870(v5, v16[1], &v15, v17);
  }
  else
  {
    *(_DWORD *)v6 = a2;
    v7 = sub_140836BC0();
    v8 = MEMORY[0x1419475D0](v7 + 32);
    v9 = (_QWORD *)v8;
    if ( v8 != 0 && *(_BYTE *)(v7 + 72) != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v7 + 64));
    if ( v8 == 0 )
      v9 = (_QWORD *)sub_1412D31C0(
                       v7,
                       *(unsigned int *)(v7 + 80),
                       *(unsigned int *)(v7 + 4LL * (*(_DWORD *)(v7 + 56) != 0) + 84));
    if ( v9 != nullptr && *(_BYTE *)(v7 + 96) != 0 )
      sub_141758A10(v9, 0, *(unsigned int *)(v7 + 80));
    v10 = v17;
    v11 = *v17;
    v12 = v17[1];
    v9[1] = v12;
    *v9 = v11;
    v13 = sub_14083D4F0(v12);
    v10[1] = 0;
    *v10 = v13 + 8;
    *(_QWORD *)(v6 + 8) = v9;
    v16[1] += 16LL;
  }
  (*(void (__fastcall **)(_QWORD))(*(_QWORD *)*v17 + 16LL))(*v17);
  return v16;
}
