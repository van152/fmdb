char __fastcall sub_140E55A60(__int64 a1, __int64 a2, unsigned __int64 *a3)
{
  __int64 *v4; // rdi
  __int64 v5; // rax
  __int64 v6; // rcx
  __int64 v7; // rax
  unsigned __int64 v8; // rax
  __int64 v9; // rcx
  int v10; // eax
  int v11; // ecx
  char v12; // bl
  unsigned __int64 v13; // rax
  int v14; // edi
  unsigned __int64 v15; // rax
  int v16; // xmm6_4
  unsigned __int64 v17; // rax
  __int64 v18; // rcx
  int v19; // eax
  int v20; // ecx
  int v21; // edi
  unsigned __int64 v22; // rax
  int v23; // xmm6_4
  unsigned __int64 v24; // rax
  __int64 v25; // rcx
  int v26; // eax
  int v27; // ecx
  __int64 v28; // rcx
  int v29; // eax
  int v30; // ecx
  int v31; // edi
  unsigned __int64 v32; // rax
  __int64 v34; // rdx
  unsigned __int64 v35; // [rsp+28h] [rbp-28h] BYREF
  _QWORD v36[2]; // [rsp+30h] [rbp-20h] BYREF

  v36[1] = -2;
  if ( (int)a2 <= 1131179885 )
  {
    if ( (int)a2 <= 1130983015 )
    {
      if ( (_DWORD)a2 == 1130458228 )
      {
        v31 = *(__int16 *)(a1 + 80);
        v7 = sub_14083D4F0() + 40;
        LODWORD(v36[0]) = v31;
        v35 = v7;
        if ( &v35 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v32 = v35;
          a3[1] = v36[0];
          *a3 = v32;
          v7 = sub_14083D4F0() + 8;
          v36[0] = 0;
          v35 = v7;
        }
        goto LABEL_26;
      }
      if ( (_DWORD)a2 == 1130460276 )
      {
        v14 = *(char *)(a1 + 84);
        v7 = sub_14083D4F0() + 40;
        LODWORD(v36[0]) = v14;
        v35 = v7;
        if ( &v35 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v15 = v35;
          a3[1] = v36[0];
          *a3 = v15;
          v7 = sub_14083D4F0() + 8;
          v36[0] = 0;
          v35 = v7;
        }
        goto LABEL_26;
      }
    }
    else
    {
      switch ( (_DWORD)a2 )
      {
        case 0x43696E68:
          v21 = *(char *)(a1 + 82);
          v7 = sub_14083D4F0() + 40;
          LODWORD(v36[0]) = v21;
          v35 = v7;
          if ( &v35 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v22 = v35;
            a3[1] = v36[0];
            *a3 = v22;
            v7 = sub_14083D4F0() + 8;
            v36[0] = 0;
            v35 = v7;
          }
          goto LABEL_26;
        case 0x436C6174:
          v23 = *(_DWORD *)(a1 + 72);
          v7 = sub_14083D4F0() + 104;
          LODWORD(v36[0]) = v23;
          v35 = v7;
          if ( &v35 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v24 = v35;
            a3[1] = v36[0];
            *a3 = v24;
            v7 = sub_14083D4F0() + 8;
            v36[0] = 0;
            v35 = v7;
          }
          goto LABEL_26;
        case 0x436C6769:
          v9 = *(_QWORD *)(a1 + 48);
          if ( v9 != 0 )
          {
            v10 = *(_DWORD *)(v9 + 12);
            v11 = *(_DWORD *)(v9 + 16);
            if ( v11 == 0 )
              v11 = v10;
          }
          else
          {
            v10 = -1;
            v11 = -1;
          }
          v35 = __PAIR64__(v11, v10);
          v34 = 1818324583;
          goto LABEL_65;
        default:
          break;
      }
    }
    return sub_140FE3F20(a1, a2, a3);
  }
  if ( (int)a2 > 1131312232 )
  {
    switch ( (_DWORD)a2 )
    {
      case 0x436E7469:
        v25 = *(_QWORD *)(a1 + 32);
        if ( v25 != 0 )
        {
          v26 = *(_DWORD *)(v25 + 12);
          v27 = *(_DWORD *)(v25 + 16);
          if ( v27 == 0 )
            v27 = v26;
        }
        else
        {
          v26 = -1;
          v27 = -1;
        }
        v35 = __PAIR64__(v27, v26);
        v34 = 1315856756;
        goto LABEL_65;
      case 0x43776561:
        v28 = *(_QWORD *)(a1 + 40);
        if ( v28 != 0 )
        {
          v29 = *(_DWORD *)(v28 + 12);
          v30 = *(_DWORD *)(v28 + 16);
          if ( v30 == 0 )
            v30 = v29;
        }
        else
        {
          v29 = -1;
          v30 = -1;
        }
        v35 = __PAIR64__(v30, v29);
        v34 = 2004117618;
        goto LABEL_65;
      case 0x44454C45:
        v12 = *(_BYTE *)(a1 + 85) & 1;
        v7 = sub_14083D4F0() + 24;
        LOBYTE(v36[0]) = v12;
        v35 = v7;
        if ( &v35 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v13 = v35;
          a3[1] = v36[0];
          *a3 = v13;
          v7 = sub_14083D4F0() + 8;
          v36[0] = 0;
          v35 = v7;
        }
        goto LABEL_26;
      default:
        break;
    }
    return sub_140FE3F20(a1, a2, a3);
  }
  if ( (_DWORD)a2 == 1131179886 )
  {
    v16 = *(_DWORD *)(a1 + 76);
    v7 = sub_14083D4F0() + 104;
    LODWORD(v36[0]) = v16;
    v35 = v7;
    if ( &v35 != a3 )
    {
      (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v17 = v35;
      a3[1] = v36[0];
      *a3 = v17;
      v7 = sub_14083D4F0() + 8;
      v36[0] = 0;
      v35 = v7;
    }
    goto LABEL_26;
  }
  if ( (_DWORD)a2 == 1131180649 )
  {
    v18 = *(_QWORD *)(a1 + 56);
    if ( v18 != 0 )
    {
      v19 = *(_DWORD *)(v18 + 12);
      v20 = *(_DWORD *)(v18 + 16);
      if ( v20 == 0 )
        v20 = v19;
    }
    else
    {
      v19 = -1;
      v20 = -1;
    }
    v35 = __PAIR64__(v20, v19);
    v34 = 1818456679;
LABEL_65:
    sub_140FE72B0(&v35, v34, a3);
    return 1;
  }
  if ( (_DWORD)a2 != 1131307373 )
    return sub_140FE3F20(a1, a2, a3);
  v4 = (__int64 *)(a1 + 24);
  v5 = sub_14083D4F0();
  v36[0] = 0;
  if ( v36 != v4 )
  {
    v6 = *v4;
    if ( *v4 != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v6 - 4));
    v36[0] = v6;
  }
  v7 = v5 + 136;
  v35 = v7;
  if ( &v35 != a3 )
  {
    (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
    v8 = v35;
    a3[1] = v36[0];
    *a3 = v8;
    v7 = sub_14083D4F0() + 8;
    v36[0] = 0;
    v35 = v7;
  }
LABEL_26:
  (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v7 + 16LL))(v7, &v35);
  return 1;
}
