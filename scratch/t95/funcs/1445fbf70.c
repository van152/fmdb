char __fastcall sub_1445FBF70(_BYTE *a1, _QWORD *a2)
{
  __int64 *v3; // rsi
  __int64 *v4; // rdi
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 *v7; // rbx
  int v8; // r12d
  __int64 v9; // rcx
  __int64 v10; // rdx
  __int64 *v11; // rax
  int v12; // eax
  char v13; // r8
  __int64 v14; // r9
  __int64 *v15; // r15
  __int64 v16; // rdx
  __int64 *v17; // rcx
  __int64 *v18; // rbp
  __int64 v19; // rcx
  __int64 v20; // r13
  unsigned __int64 v21; // rcx
  __int64 v22; // r11
  __int64 v23; // rbx
  __int64 v24; // rcx
  __int64 *v25; // r14
  __int64 v26; // rdi
  int v27; // ebp
  __int64 v28; // rbx
  __int64 v29; // rcx
  __int64 v30; // rcx
  _QWORD *v32; // [rsp+20h] [rbp-48h]

  v3 = nullptr;
  v4 = (__int64 *)(*(__int64 (__fastcall **)(_QWORD, _QWORD *, _QWORD))(*(_QWORD *)*a2 + 176LL))(*a2, a2, 0);
  v5 = *v4;
  v6 = v4[1];
  if ( *v4 != v6 )
  {
    v3 = nullptr;
    while ( *(_DWORD *)v5 != 1685353593 )
    {
      v5 += 16;
      if ( v5 == v6 )
        goto LABEL_9;
    }
    if ( v5 == v6 )
      v3 = nullptr;
    else
      v3 = *(__int64 **)(v5 + 8);
  }
LABEL_9:
  v7 = &qword_141B5A4A0;
  if ( v3 == nullptr )
    v3 = &qword_141B5A4A0;
  v8 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v3 + 64LL))(*v3, v3);
  v9 = *v4;
  v10 = v4[1];
  v11 = nullptr;
  if ( *v4 != v10 )
  {
    while ( *(_DWORD *)v9 != 1685417577 )
    {
      v9 += 16;
      if ( v9 == v10 )
        goto LABEL_18;
    }
    if ( v9 == v10 )
      v11 = nullptr;
    else
      v11 = *(__int64 **)(v9 + 8);
  }
LABEL_18:
  if ( v11 != nullptr )
    v7 = v11;
  v12 = (*(__int64 (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*v7 + 64LL))(*v7, v7);
  v13 = a1[16];
  v14 = *(_QWORD *)a1;
  v15 = (__int64 *)(*(_QWORD *)a1 + 152LL);
  v16 = *(_QWORD *)a1 + 144LL;
  v17 = v15;
  v32 = (_QWORD *)(*(_QWORD *)a1 + 176LL);
  if ( v13 == 0 )
    v17 = (__int64 *)(*(_QWORD *)a1 + 176LL);
  v18 = (__int64 *)(v14 + 168);
  v19 = *v17;
  if ( v13 != 0 )
    v18 = (__int64 *)(*(_QWORD *)a1 + 144LL);
  v20 = *v18;
  v21 = (unsigned __int64)(v19 - *v18) >> 3;
  if ( (int)v21 > 0 )
  {
    v22 = (unsigned int)v21;
    v23 = 0;
    v24 = 0;
    while ( 1 )
    {
      v25 = *(__int64 **)(v20 + 8 * v24);
      v26 = *v25;
      v27 = 9;
      if ( *v25 != 0
        || (v26 = v25[1], v27 = 5, v26 != 0)
        || (v26 = v25[3], v27 = 19, v26 != 0)
        || (v26 = v25[4], v27 = 56, v26 != 0) )
      {
        LODWORD(v16) = *(_DWORD *)(v26 + 12);
        LODWORD(v3) = v27;
      }
      if ( (_DWORD)v3 == v8 && (_DWORD)v16 == v12 )
        break;
      ++v24;
      v23 += 0x100000000LL;
      if ( v22 == v24 )
        return 1;
    }
    v28 = v23 >> 32;
    if ( v13 != 0 )
    {
      v29 = *(_QWORD *)(*(_QWORD *)(v14 + 144) + 8 * v28);
      if ( v29 != 0 )
        sub_141750CFC(v29);
      sub_141758A00();
      *v15 -= 8;
    }
    else
    {
      v30 = *(_QWORD *)(*(_QWORD *)(v14 + 168) + 8 * v28);
      if ( v30 != 0 )
        sub_141750CFC(v30);
      sub_141758A00();
      *v32 -= 8LL;
    }
  }
  return 1;
}
