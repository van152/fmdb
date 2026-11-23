char __fastcall sub_140FFDBB0(__int64 a1, int a2, __int64 *a3)
{
  __int64 *v5; // rdi
  __int64 v6; // rax
  __int64 v7; // rcx
  __int64 v8; // rax
  __int64 *v9; // rax
  __int64 v10; // rcx
  int v11; // edi
  __int64 *v12; // rax
  __int64 v13; // rcx
  int v14; // edi
  __int64 *v15; // rax
  __int64 v16; // rcx
  __int64 v17; // rcx
  int v18; // eax
  int v19; // ecx
  __int64 *v20; // rdi
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 *v23; // rax
  __int64 v24; // rcx
  __int64 *v25; // rdi
  __int64 v26; // rax
  __int64 v27; // rcx
  __int64 *v28; // rax
  __int64 v29; // rcx
  __int64 *v31; // rdi
  __int64 v32; // rax
  __int64 v33; // rcx
  __int64 *v34; // rax
  __int64 v35; // rcx
  __int64 v36; // rdx
  __int64 *v37; // rdi
  __int64 v38; // rax
  __int64 v39; // rcx
  __int64 *v40; // rax
  __int64 v41; // rcx
  _DWORD *v42; // rdi
  int v43; // esi
  int v44; // edi
  int v45; // eax
  int v46; // esi
  bool v47; // zf
  int v48; // eax
  __int64 v49; // rcx
  __int64 v50; // rax
  __int64 v51; // rcx
  __int64 v52; // rcx
  int v53; // eax
  int v54; // ecx
  __int64 *v55; // rcx
  __int64 *v56; // rax
  __int64 v57; // rcx
  __int64 v58; // rcx
  int v59; // eax
  int v60; // ecx
  __int64 v61; // [rsp+20h] [rbp-30h] BYREF
  __int64 v62; // [rsp+28h] [rbp-28h]
  __int64 *v63; // [rsp+30h] [rbp-20h] BYREF
  _QWORD v64[9]; // [rsp+38h] [rbp-18h] BYREF

  v64[2] = -2;
  if ( a2 <= 1148084588 )
  {
    if ( a2 > 1147561776 )
    {
      switch ( a2 )
      {
        case 1147563361:
          if ( *(int *)(a1 + 100) < 0 )
          {
            (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
              qword_141B5A4A0,
              &qword_141B5A4A0,
              &v63);
          }
          else
          {
            LODWORD(v64[0]) = *(_DWORD *)(a1 + 100);
            v63 = (__int64 *)(sub_14083D4F0(a1) + 40);
          }
          if ( &v63 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            (*(void (__fastcall **)(__int64 *, __int64 **, __int64 *))(*v63 + 24))(v63, &v63, a3);
          }
          break;
        case 1147563362:
        case 1147563365:
        case 1147563366:
        case 1147563367:
        case 1147563368:
        case 1147563369:
        case 1147563370:
        case 1147563371:
        case 1147563372:
        case 1147563373:
        case 1147563374:
        case 1147563375:
        case 1147563376:
        case 1147563377:
        case 1147563378:
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        case 1147563363:
          v52 = *(_QWORD *)(a1 + 80);
          if ( v52 != 0 )
          {
            v53 = *(_DWORD *)(v52 + 12);
            v54 = *(_DWORD *)(v52 + 16);
            if ( v54 == 0 )
              v54 = v53;
          }
          else
          {
            v53 = -1;
            v54 = -1;
          }
          v63 = (__int64 *)__PAIR64__(v54, v53);
          v36 = 1668246896;
          goto LABEL_122;
        case 1147563364:
          if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(&dword_141B5C8D0);
            if ( dword_141B5C8D0 == -1 )
            {
              sub_140DBC9B0(&qword_141B5C8A0);
              sub_141751048(sub_140DBCA10);
              sub_141750EA0(&dword_141B5C8D0);
            }
          }
          LODWORD(v64[0]) = ((*(_WORD *)(a1 + 96) & 0x1FF) << 8)
                          | (*(unsigned __int16 *)(a1 + 96) >> 9)
                          | (*(unsigned __int16 *)(a1 + 98) << 17);
          v55 = &qword_141B5C8A0;
          v63 = &qword_141B5C8A0;
          if ( &v63 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v56 = v63;
            v57 = v64[0];
            a3[1] = v64[0];
            *a3 = (__int64)v56;
            v55 = (__int64 *)(sub_14083D4F0(v57) + 8);
            v64[0] = 0;
            v63 = v55;
          }
          (*(void (__fastcall **)(__int64 *, __int64 **))(*v55 + 16))(v55, &v63);
          return 1;
        case 1147563379:
          v58 = *(_QWORD *)(a1 + 88);
          if ( v58 != 0 )
          {
            v59 = *(_DWORD *)(v58 + 12);
            v60 = *(_DWORD *)(v58 + 16);
            if ( v60 == 0 )
              v60 = v59;
          }
          else
          {
            v59 = -1;
            v60 = -1;
          }
          v63 = (__int64 *)__PAIR64__(v60, v59);
          v36 = 1937006948;
          goto LABEL_122;
        default:
          if ( a2 == 1147561777 )
          {
            if ( *(char *)(a1 + 118) < 0 )
            {
              (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                qword_141B5A4A0,
                &qword_141B5A4A0,
                &v63);
            }
            else
            {
              LODWORD(v64[0]) = *(unsigned __int8 *)(a1 + 118);
              v63 = (__int64 *)(sub_14083D4F0(a1) + 40);
            }
            if ( &v63 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              (*(void (__fastcall **)(__int64 *, __int64 **, __int64 *))(*v63 + 24))(v63, &v63, a3);
            }
          }
          else
          {
            if ( a2 != 1147561778 )
              return sub_140FE3F20((_DWORD *)a1, a2, a3);
            if ( *(char *)(a1 + 119) < 0 )
            {
              (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
                qword_141B5A4A0,
                &qword_141B5A4A0,
                &v63);
            }
            else
            {
              LODWORD(v64[0]) = *(unsigned __int8 *)(a1 + 119);
              v63 = (__int64 *)(sub_14083D4F0(a1) + 40);
            }
            if ( &v63 != (__int64 **)a3 )
            {
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
              (*(void (__fastcall **)(__int64 *, __int64 **, __int64 *))(*v63 + 24))(v63, &v63, a3);
            }
          }
          break;
      }
    }
    else if ( a2 <= 1144091766 )
    {
      if ( a2 == 1144091748 )
      {
        if ( *(__int16 *)(a1 + 114) < 0 )
        {
          (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
            qword_141B5A4A0,
            &qword_141B5A4A0,
            &v63);
        }
        else
        {
          LODWORD(v64[0]) = *(unsigned __int16 *)(a1 + 114);
          v63 = (__int64 *)(sub_14083D4F0(a1) + 40);
        }
        if ( &v63 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          (*(void (__fastcall **)(__int64 *, __int64 **, __int64 *))(*v63 + 24))(v63, &v63, a3);
        }
      }
      else
      {
        if ( a2 != 1144091756 )
          return sub_140FE3F20((_DWORD *)a1, a2, a3);
        if ( *(__int16 *)(a1 + 116) < 0 )
        {
          (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
            qword_141B5A4A0,
            &qword_141B5A4A0,
            &v63);
        }
        else
        {
          LODWORD(v64[0]) = *(unsigned __int16 *)(a1 + 116);
          v63 = (__int64 *)(sub_14083D4F0(a1) + 40);
        }
        if ( &v63 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          (*(void (__fastcall **)(__int64 *, __int64 **, __int64 *))(*v63 + 24))(v63, &v63, a3);
        }
      }
    }
    else
    {
      if ( a2 != 1144091767 )
      {
        if ( a2 == 1147235949 )
        {
          v25 = (__int64 *)(a1 + 48);
          v26 = sub_14083D4F0(a1);
          v64[0] = 0;
          if ( v64 != v25 )
          {
            v27 = *v25;
            if ( *v25 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v27 - 4));
            v64[0] = v27;
          }
          v8 = v26 + 136;
          v63 = (__int64 *)v8;
          if ( &v63 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v28 = v63;
            v29 = v64[0];
            a3[1] = v64[0];
            *a3 = (__int64)v28;
            v8 = sub_14083D4F0(v29) + 8;
            v64[0] = 0;
            v63 = (__int64 *)v8;
          }
          goto LABEL_80;
        }
        if ( a2 == 1147237230 )
        {
          v5 = (__int64 *)(a1 + 40);
          v6 = sub_14083D4F0(a1);
          v64[0] = 0;
          if ( v64 != v5 )
          {
            v7 = *v5;
            if ( *v5 != 0 )
              _InterlockedIncrement((volatile signed __int32 *)(v7 - 4));
            v64[0] = v7;
          }
          v8 = v6 + 136;
          v63 = (__int64 *)v8;
          if ( &v63 != (__int64 **)a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v9 = v63;
            v10 = v64[0];
            a3[1] = v64[0];
            *a3 = (__int64)v9;
            v8 = sub_14083D4F0(v10) + 8;
            v64[0] = 0;
            v63 = (__int64 *)v8;
          }
LABEL_80:
          (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v8 + 16LL))(v8, &v63);
          return 1;
        }
        return sub_140FE3F20((_DWORD *)a1, a2, a3);
      }
      if ( *(__int16 *)(a1 + 112) < 0 )
      {
        (*(void (__fastcall **)(__int64, __int64 *, __int64 **))(*(_QWORD *)qword_141B5A4A0 + 24LL))(
          qword_141B5A4A0,
          &qword_141B5A4A0,
          &v63);
      }
      else
      {
        LODWORD(v64[0]) = *(unsigned __int16 *)(a1 + 112);
        v63 = (__int64 *)(sub_14083D4F0(a1) + 40);
      }
      if ( &v63 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        (*(void (__fastcall **)(__int64 *, __int64 **, __int64 *))(*v63 + 24))(v63, &v63, a3);
      }
    }
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v63 + 16))(v63, &v63);
    return 1;
  }
  if ( a2 <= 1148480817 )
  {
    if ( a2 <= 1148415596 )
    {
      if ( a2 == 1148084589 )
      {
        v31 = (__int64 *)(a1 + 24);
        v32 = sub_14083D4F0(a1);
        v64[0] = 0;
        if ( v64 != v31 )
        {
          v33 = *v31;
          if ( *v31 != 0 )
            _InterlockedIncrement((volatile signed __int32 *)(v33 - 4));
          v64[0] = v33;
        }
        v8 = v32 + 136;
        v63 = (__int64 *)v8;
        if ( &v63 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v34 = v63;
          v35 = v64[0];
          a3[1] = v64[0];
          *a3 = (__int64)v34;
          v8 = sub_14083D4F0(v35) + 8;
          v64[0] = 0;
          v63 = (__int64 *)v8;
        }
        goto LABEL_80;
      }
      if ( a2 == 1148089458 )
      {
        v11 = *(unsigned __int8 *)(a1 + 125);
        v8 = sub_14083D4F0(a1) + 56;
        LODWORD(v64[0]) = v11;
        v63 = (__int64 *)v8;
        if ( &v63 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v12 = v63;
          v13 = v64[0];
          a3[1] = v64[0];
          *a3 = (__int64)v12;
          v8 = sub_14083D4F0(v13) + 8;
          v64[0] = 0;
          v63 = (__int64 *)v8;
        }
        goto LABEL_80;
      }
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    }
    if ( a2 == 1148415597 )
    {
      v37 = (__int64 *)(a1 + 32);
      v38 = sub_14083D4F0(a1);
      v64[0] = 0;
      if ( v64 != v37 )
      {
        v39 = *v37;
        if ( *v37 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v39 - 4));
        v64[0] = v39;
      }
      v8 = v38 + 136;
      v63 = (__int64 *)v8;
      if ( &v63 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v40 = v63;
        v41 = v64[0];
        a3[1] = v64[0];
        *a3 = (__int64)v40;
        v8 = sub_14083D4F0(v41) + 8;
        v64[0] = 0;
        v63 = (__int64 *)v8;
      }
      goto LABEL_80;
    }
    if ( a2 != 1148480817 )
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    v17 = *(_QWORD *)(a1 + 64);
    if ( v17 == 0 )
      goto LABEL_37;
    goto LABEL_71;
  }
  if ( a2 <= 1684172396 )
  {
    if ( a2 != 1148480818 )
    {
      if ( a2 == 1148675186 )
      {
        v14 = *(unsigned __int8 *)(a1 + 124);
        v8 = sub_14083D4F0(a1) + 56;
        LODWORD(v64[0]) = v14;
        v63 = (__int64 *)v8;
        if ( &v63 != (__int64 **)a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v15 = v63;
          v16 = v64[0];
          a3[1] = v64[0];
          *a3 = (__int64)v15;
          v8 = sub_14083D4F0(v16) + 8;
          v64[0] = 0;
          v63 = (__int64 *)v8;
        }
        goto LABEL_80;
      }
      return sub_140FE3F20((_DWORD *)a1, a2, a3);
    }
    v17 = *(_QWORD *)(a1 + 72);
    if ( v17 == 0 )
    {
LABEL_37:
      v18 = -1;
      v19 = -1;
LABEL_73:
      v63 = (__int64 *)__PAIR64__(v19, v18);
      v36 = 1416914273;
LABEL_122:
      sub_140FE72B0(&v63, v36, a3);
      return 1;
    }
LABEL_71:
    v18 = *(_DWORD *)(v17 + 12);
    v19 = *(_DWORD *)(v17 + 16);
    if ( v19 == 0 )
      v19 = v18;
    goto LABEL_73;
  }
  if ( a2 != 1919968370 )
  {
    if ( a2 == 1684172397 )
    {
      v20 = (__int64 *)(a1 + 24);
      v21 = sub_14083D4F0(a1);
      v64[0] = 0;
      if ( v64 != v20 )
      {
        v22 = *v20;
        if ( *v20 != 0 )
          _InterlockedIncrement((volatile signed __int32 *)(v22 - 4));
        v64[0] = v22;
      }
      v8 = v21 + 136;
      v63 = (__int64 *)v8;
      if ( &v63 != (__int64 **)a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v23 = v63;
        v24 = v64[0];
        a3[1] = v64[0];
        *a3 = (__int64)v23;
        v8 = sub_14083D4F0(v24) + 8;
        v64[0] = 0;
        v63 = (__int64 *)v8;
      }
      goto LABEL_80;
    }
    return sub_140FE3F20((_DWORD *)a1, a2, a3);
  }
  v42 = *(_DWORD **)(a1 + 104);
  if ( v42 == nullptr )
    return 0;
  v62 = 0;
  v61 = sub_14083D4F0(a1) + 8;
  v43 = v42[2];
  v44 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v42 + 56LL))(v42);
  (*(void (__fastcall **)(__int64, __int64 *, _QWORD *))(*(_QWORD *)v61 + 24LL))(v61, &v61, v64);
  v45 = v43 & v44;
  v46 = (v44 << 24) | v43 & 0x7FFFFF;
  v47 = v45 == -1;
  v48 = -8388609;
  if ( !v47 )
    v48 = v46;
  LODWORD(v63) = v48;
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v61 + 16LL))(v61, &v61);
  sub_140FEAD00(&v63, &v61);
  v49 = *a3;
  if ( &v61 != a3 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v49 + 16LL))(v49, a3);
    v50 = v61;
    v51 = v62;
    a3[1] = v62;
    *a3 = v50;
    v49 = sub_14083D4F0(v51) + 8;
    v62 = 0;
    v61 = v49;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v49 + 16LL))(v49, &v61);
  (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v64[0] + 16LL))(v64[0], v64);
  return 1;
}
