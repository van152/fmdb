char __fastcall sub_141568D60(__int64 a1, int a2, __int64 **a3)
{
  char result; // al
  char v6; // bl
  __int64 v7; // rax
  __int64 *v8; // rax
  __int64 *v9; // rcx
  int v10; // edi
  __int64 *v11; // rax
  __int64 *v12; // rcx
  __int64 v13; // rcx
  __int64 v14; // rcx
  int v15; // eax
  int v16; // ecx
  int v17; // edi
  __int64 *v18; // rax
  __int64 *v19; // rcx
  char v20; // bl
  __int64 *v21; // rax
  __int64 *v22; // rcx
  int v23; // edi
  __int64 *v24; // rax
  __int64 *v25; // rcx
  char v26; // bl
  __int64 *v27; // rax
  __int64 *v28; // rcx
  int v29; // edi
  __int64 *v30; // rax
  __int64 *v31; // rcx
  int v32; // eax
  int v33; // ecx
  __int64 *v34; // rcx
  __int64 *v35; // rax
  __int64 *v36; // rcx
  char v37; // bl
  __int64 *v38; // rax
  __int64 *v39; // rcx
  __int64 v40; // rcx
  int v41; // eax
  int v42; // ecx
  int v43; // edi
  __int64 *v44; // rax
  __int64 *v45; // rcx
  char v46; // bl
  __int64 *v47; // rax
  __int64 *v48; // rcx
  __int64 v49; // rdx
  int v50; // edi
  __int64 *v51; // rax
  __int64 *v52; // rcx
  __int64 *v53; // rax
  __int64 *v54; // rcx
  __int64 *v55; // [rsp+20h] [rbp-10h] BYREF
  __int64 *v56; // [rsp+28h] [rbp-8h]
  __int64 v57; // [rsp+30h] [rbp+0h]

  v57 = -2;
  result = 0;
  if ( a2 > 1752396848 )
  {
    if ( a2 <= 1886150962 )
    {
      if ( a2 <= 1752396850 )
      {
        if ( a2 == 1752396849 )
        {
          v13 = *(_QWORD *)(a1 + 72);
          if ( v13 != 0 )
            goto LABEL_64;
        }
        else
        {
          v13 = *(_QWORD *)(a1 + 80);
          if ( v13 != 0 )
            goto LABEL_64;
        }
      }
      else
      {
        switch ( a2 )
        {
          case 1752396851:
            v13 = *(_QWORD *)(a1 + 88);
            if ( v13 != 0 )
              goto LABEL_64;
            break;
          case 1886150961:
            v13 = *(_QWORD *)(a1 + 32);
            if ( v13 != 0 )
              goto LABEL_64;
            break;
          case 1886150962:
            v13 = *(_QWORD *)(a1 + 40);
            if ( v13 != 0 )
              goto LABEL_64;
            break;
          default:
            return result;
        }
      }
    }
    else
    {
      if ( a2 > 1937008493 )
      {
        if ( a2 != 1937008494 )
        {
          if ( a2 == 2037542770 )
          {
            v43 = *(char *)(a1 + 118);
            v7 = sub_14083D4F0(a1) + 40;
            LODWORD(v56) = v43;
            v55 = (__int64 *)v7;
            if ( &v55 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v44 = v55;
              v45 = v56;
              a3[1] = v56;
              *a3 = v44;
              v7 = sub_14083D4F0(v45) + 8;
              v56 = nullptr;
              v55 = (__int64 *)v7;
            }
          }
          else
          {
            if ( a2 != 2036687218 )
              return result;
            v17 = *(__int16 *)(a1 + 108);
            v7 = sub_14083D4F0(a1) + 40;
            LODWORD(v56) = v17;
            v55 = (__int64 *)v7;
            if ( &v55 != a3 )
            {
              (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
              v18 = v55;
              v19 = v56;
              a3[1] = v56;
              *a3 = v18;
              v7 = sub_14083D4F0(v19) + 8;
              v56 = nullptr;
              v55 = (__int64 *)v7;
            }
          }
          goto LABEL_37;
        }
        v40 = *(_QWORD *)(a1 + 96);
        if ( v40 != 0 )
        {
          v41 = *(_DWORD *)(v40 + 12);
          v42 = *(_DWORD *)(v40 + 16);
          if ( v42 == 0 )
            v42 = v41;
        }
        else
        {
          v41 = -1;
          v42 = -1;
        }
        v55 = (__int64 *)__PAIR64__(v42, v41);
        v49 = 1937008494;
LABEL_87:
        sub_140FE72B0(&v55, v49, a3);
        return 1;
      }
      if ( a2 != 1886150963 )
      {
        if ( a2 != 1886156654 )
        {
          if ( a2 != 1936289383 )
            return result;
          v6 = *(_BYTE *)(a1 + 116);
          v7 = sub_14083D4F0(a1) + 24;
          LOBYTE(v56) = (v6 & 2) != 0;
          v55 = (__int64 *)v7;
          if ( &v55 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v8 = v55;
            v9 = v56;
            a3[1] = v56;
            *a3 = v8;
            v7 = sub_14083D4F0(v9) + 8;
            v56 = nullptr;
            v55 = (__int64 *)v7;
          }
          goto LABEL_37;
        }
        v13 = *(_QWORD *)(a1 + 56);
        if ( v13 == 0 )
          goto LABEL_85;
LABEL_64:
        v32 = *(_DWORD *)(v13 + 12);
        v33 = *(_DWORD *)(v13 + 16);
        if ( v33 == 0 )
          v33 = v32;
        goto LABEL_86;
      }
      v13 = *(_QWORD *)(a1 + 48);
      if ( v13 != 0 )
        goto LABEL_64;
    }
LABEL_85:
    v32 = -1;
    v33 = -1;
LABEL_86:
    v55 = (__int64 *)__PAIR64__(v33, v32);
    v49 = 1416914273;
    goto LABEL_87;
  }
  if ( a2 <= 1667789925 )
  {
    if ( a2 <= 1667526259 )
    {
      if ( a2 == 1633907311 )
      {
        v46 = *(_BYTE *)(a1 + 116);
        v7 = sub_14083D4F0(a1) + 24;
        LOBYTE(v56) = (v46 & 4) != 0;
        v55 = (__int64 *)v7;
        if ( &v55 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v47 = v55;
          v48 = v56;
          a3[1] = v56;
          *a3 = v47;
          v7 = sub_14083D4F0(v48) + 8;
          v56 = nullptr;
          v55 = (__int64 *)v7;
        }
      }
      else
      {
        if ( a2 != 1667526246 )
          return result;
        v20 = *(_BYTE *)(a1 + 117);
        v7 = sub_14083D4F0(a1) + 24;
        LOBYTE(v56) = v20 & 1;
        v55 = (__int64 *)v7;
        if ( &v55 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v21 = v55;
          v22 = v56;
          a3[1] = v56;
          *a3 = v21;
          v7 = sub_14083D4F0(v22) + 8;
          v56 = nullptr;
          v55 = (__int64 *)v7;
        }
      }
    }
    else
    {
      switch ( a2 )
      {
        case 1667526260:
          v26 = *(_BYTE *)(a1 + 116);
          v7 = sub_14083D4F0(a1) + 24;
          LOBYTE(v56) = (v26 & 8) != 0;
          v55 = (__int64 *)v7;
          if ( &v55 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v27 = v55;
            v28 = v56;
            a3[1] = v56;
            *a3 = v27;
            v7 = sub_14083D4F0(v28) + 8;
            v56 = nullptr;
            v55 = (__int64 *)v7;
          }
          break;
        case 1667786105:
          v29 = *(__int16 *)(a1 + 114);
          v7 = sub_14083D4F0(a1) + 40;
          LODWORD(v56) = v29;
          v55 = (__int64 *)v7;
          if ( &v55 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v30 = v55;
            v31 = v56;
            a3[1] = v56;
            *a3 = v30;
            v7 = sub_14083D4F0(v31) + 8;
            v56 = nullptr;
            v55 = (__int64 *)v7;
          }
          break;
        case 1667789689:
          v10 = *(__int16 *)(a1 + 112);
          v7 = sub_14083D4F0(a1) + 40;
          LODWORD(v56) = v10;
          v55 = (__int64 *)v7;
          if ( &v55 != a3 )
          {
            (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
            v11 = v55;
            v12 = v56;
            a3[1] = v56;
            *a3 = v11;
            v7 = sub_14083D4F0(v12) + 8;
            v56 = nullptr;
            v55 = (__int64 *)v7;
          }
          break;
        default:
          return result;
      }
    }
    goto LABEL_37;
  }
  if ( a2 <= 1685349474 )
  {
    if ( a2 == 1667789926 )
    {
      v50 = *(unsigned __int16 *)(a1 + 116);
      if ( v50 == 255 )
      {
        v7 = sub_14083D4F0(a1) + 24;
        LOBYTE(v56) = 0;
        v55 = (__int64 *)v7;
        if ( &v55 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v51 = v55;
          v52 = v56;
          a3[1] = v56;
          *a3 = v51;
          v7 = sub_14083D4F0(v52) + 8;
          v56 = nullptr;
          v55 = (__int64 *)v7;
        }
      }
      else
      {
        v7 = sub_14083D4F0(a1) + 40;
        LODWORD(v56) = v50 & 0x36;
        v55 = (__int64 *)v7;
        if ( &v55 != a3 )
        {
          (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
          v53 = v55;
          v54 = v56;
          a3[1] = v56;
          *a3 = v53;
          v7 = sub_14083D4F0(v54) + 8;
          v56 = nullptr;
          v55 = (__int64 *)v7;
        }
      }
    }
    else
    {
      if ( a2 != 1668181860 )
        return result;
      v23 = *(unsigned __int16 *)(a1 + 116);
      v7 = sub_14083D4F0(a1) + 24;
      LOBYTE(v56) = v23 == 255;
      v55 = (__int64 *)v7;
      if ( &v55 != a3 )
      {
        (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
        v24 = v55;
        v25 = v56;
        a3[1] = v56;
        *a3 = v24;
        v7 = sub_14083D4F0(v25) + 8;
        v56 = nullptr;
        v55 = (__int64 *)v7;
      }
    }
    goto LABEL_37;
  }
  if ( a2 == 1685349475 )
  {
    if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
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
    LODWORD(v56) = ((*(_WORD *)(a1 + 104) & 0x1FF) << 8)
                 | (*(unsigned __int16 *)(a1 + 104) >> 9)
                 | (*(unsigned __int16 *)(a1 + 106) << 17);
    v34 = &qword_141B5C8A0;
    v55 = &qword_141B5C8A0;
    if ( &v55 != a3 )
    {
      (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
      v35 = v55;
      v36 = v56;
      a3[1] = v56;
      *a3 = v35;
      v34 = (__int64 *)(sub_14083D4F0(v36) + 8);
      v56 = nullptr;
      v55 = v34;
    }
    (*(void (__fastcall **)(__int64 *, __int64 **))(*v34 + 16))(v34, &v55);
    return 1;
  }
  if ( a2 != 1751807095 )
  {
    if ( a2 != 1752134516 )
      return result;
    v14 = *(_QWORD *)(a1 + 64);
    if ( v14 != 0 )
    {
      v15 = *(_DWORD *)(v14 + 12);
      v16 = *(_DWORD *)(v14 + 16);
      if ( v16 == 0 )
        v16 = v15;
    }
    else
    {
      v15 = -1;
      v16 = -1;
    }
    v55 = (__int64 *)__PAIR64__(v16, v15);
    v49 = 1937006948;
    goto LABEL_87;
  }
  v37 = *(_BYTE *)(a1 + 116);
  v7 = sub_14083D4F0(a1) + 24;
  LOBYTE(v56) = v37 & 1;
  v55 = (__int64 *)v7;
  if ( &v55 != a3 )
  {
    (*(void (__fastcall **)(__int64 *, __int64 **))(**a3 + 16))(*a3, a3);
    v38 = v55;
    v39 = v56;
    a3[1] = v56;
    *a3 = v38;
    v7 = sub_14083D4F0(v39) + 8;
    v56 = nullptr;
    v55 = (__int64 *)v7;
  }
LABEL_37:
  (*(void (__fastcall **)(__int64, __int64 **))(*(_QWORD *)v7 + 16LL))(v7, &v55);
  return 1;
}
