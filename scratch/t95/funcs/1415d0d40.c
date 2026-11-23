// THUNK ALIAS -> sub_1445FC630 (jmp:0x1415d0d40->0x1445fc630)
char __fastcall sub_1445FC630(__int64 a1, _QWORD *a2)
{
  __int64 *v3; // rdi
  __int64 *v4; // rbx
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 *v7; // rsi
  int v8; // edi
  __int64 v9; // rcx
  __int64 v10; // rdx
  __int64 *v11; // rax
  unsigned int v12; // ebx
  __int64 v13; // rax
  int v14; // edx
  __int64 v15; // r8
  __int64 v16; // rsi
  unsigned int v17; // ebx

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
  v13 = 0;
  if ( v8 > 18 )
  {
    if ( v8 == 19 )
    {
      if ( v12 != -1 )
      {
        v13 = sub_140F74E40(qword_141B5FE20, v12);
LABEL_34:
        v14 = 0;
        goto LABEL_35;
      }
    }
    else
    {
      v14 = 0;
      LODWORD(v15) = 0;
      v16 = 0;
      if ( v8 != 56 )
        goto LABEL_37;
      if ( v12 != -1 )
      {
        v16 = sub_140F74650(qword_141B5FE60, v12);
        v13 = 0;
        v14 = 0;
        LODWORD(v15) = 0;
        goto LABEL_37;
      }
    }
LABEL_33:
    v13 = 0;
    goto LABEL_34;
  }
  if ( v8 == 5 )
  {
    v17 = v12 - 1;
    if ( v17 <= 6 )
    {
      v15 = *(_QWORD *)(**(_QWORD **)(qword_141B5FDC8 + 128) + 8LL * v17);
      v13 = 0;
      v14 = 0;
LABEL_36:
      v16 = 0;
      goto LABEL_37;
    }
    goto LABEL_33;
  }
  v14 = 0;
  LODWORD(v15) = 0;
  v16 = 0;
  if ( v8 == 9 )
  {
    if ( v12 != -1 )
    {
      v14 = sub_1400568B0(qword_141B5FDD0, v12);
      v13 = 0;
LABEL_35:
      LODWORD(v15) = 0;
      goto LABEL_36;
    }
    goto LABEL_33;
  }
LABEL_37:
  sub_14104D650(*(_QWORD *)a1, v14, v15, 0, v13, v16, *(_BYTE *)(a1 + 16), 124518401, 124518401);
  return 1;
}
