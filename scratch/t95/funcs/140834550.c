_QWORD *__fastcall sub_140834550(_QWORD *a1, int a2, _QWORD *a3, int a4, _QWORD *a5)
{
  _QWORD *v7; // rsi
  __int64 v8; // rdi
  __int64 v9; // rbx
  __int64 v10; // rax
  _QWORD *v11; // rsi
  _QWORD *v12; // rbx
  __int64 v13; // rax
  __int64 v14; // rcx
  __int64 v15; // rax
  _QWORD *v16; // rcx
  __int64 v17; // rdx
  __int64 v18; // rbx
  __int64 v19; // rsi
  __int64 v20; // rax
  _QWORD *v21; // rdi
  __int64 v22; // rax
  __int64 v23; // rcx
  __int64 v24; // rax
  int v26; // [rsp+20h] [rbp-20h] BYREF
  int v27; // [rsp+24h] [rbp-1Ch] BYREF
  _QWORD *v28; // [rsp+28h] [rbp-18h]
  _QWORD *v29; // [rsp+30h] [rbp-10h]
  __int64 v30; // [rsp+38h] [rbp-8h]

  v30 = -2;
  v28 = a3;
  v7 = a1;
  v29 = a1;
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
        v7 = v29;
      }
    }
    qword_141ABD470 = (__int64)&unk_141B59A68;
  }
  v7[2] = 0;
  v7[1] = 0;
  *v7 = 0;
  v27 = a2;
  sub_140837DD0(v7, 4);
  v8 = v29[1];
  if ( v8 == v29[2] )
  {
    sub_140837870(v29, v29[1], &v27, v28);
  }
  else
  {
    *(_DWORD *)v8 = a2;
    v9 = ((__int64 (*)(void))sub_140836BC0)();
    v10 = MEMORY[0x1419475D0](v9 + 32);
    v11 = (_QWORD *)v10;
    if ( v10 != 0 && *(_BYTE *)(v9 + 72) != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v9 + 64));
    if ( v10 == 0 )
      v11 = (_QWORD *)sub_1412D31C0(
                        v9,
                        *(unsigned int *)(v9 + 80),
                        *(unsigned int *)(v9 + 4LL * (*(_DWORD *)(v9 + 56) != 0) + 84));
    if ( v11 != nullptr && *(_BYTE *)(v9 + 96) != 0 )
      sub_141758A10(v11, 0, *(unsigned int *)(v9 + 80));
    v12 = v28;
    v13 = *v28;
    v14 = v28[1];
    v11[1] = v14;
    *v11 = v13;
    v15 = sub_14083D4F0(v14);
    v12[1] = 0;
    *v12 = v15 + 8;
    *(_QWORD *)(v8 + 8) = v11;
    v29[1] += 16LL;
  }
  v26 = a4;
  v16 = v29;
  v17 = v29[2];
  if ( v17 == *v29 )
  {
    sub_140837DD0(v29, 4);
    v16 = v29;
    v17 = v29[2];
  }
  v18 = v16[1];
  if ( v18 == v17 )
  {
    sub_140837870(v16, v17, &v26, a5);
  }
  else
  {
    *(_DWORD *)v18 = a4;
    v19 = sub_140836BC0(v16);
    v20 = MEMORY[0x1419475D0](v19 + 32);
    v21 = (_QWORD *)v20;
    if ( v20 != 0 && *(_BYTE *)(v19 + 72) != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v19 + 64));
    if ( v20 == 0 )
      v21 = (_QWORD *)sub_1412D31C0(
                        v19,
                        *(unsigned int *)(v19 + 80),
                        *(unsigned int *)(v19 + 4LL * (*(_DWORD *)(v19 + 56) != 0) + 84));
    if ( v21 != nullptr && *(_BYTE *)(v19 + 96) != 0 )
      sub_141758A10(v21, 0, *(unsigned int *)(v19 + 80));
    v22 = *a5;
    v23 = a5[1];
    v21[1] = v23;
    *v21 = v22;
    v24 = sub_14083D4F0(v23);
    a5[1] = 0;
    *a5 = v24 + 8;
    *(_QWORD *)(v18 + 8) = v21;
    v29[1] += 16LL;
  }
  (*(void (__fastcall **)(_QWORD))(*(_QWORD *)*v28 + 16LL))(*v28);
  (*(void (__fastcall **)(_QWORD))(*(_QWORD *)*a5 + 16LL))(*a5);
  return v29;
}
