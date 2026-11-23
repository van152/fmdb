char __fastcall sub_141520A50(int *a1, int a2, __int64 *a3)
{
  char result; // al
  __int16 v5; // di
  __int16 v6; // r14
  int v7; // ebx
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rcx
  int v11; // edi
  __int64 v12; // rax
  __int64 v13; // rcx
  int v14; // edi
  __int64 v15; // rax
  __int64 v16; // rcx
  int v17; // edi
  __int64 v18; // rax
  __int64 v19; // rcx
  int v20; // edi
  __int64 v21; // rax
  __int64 v22; // rcx
  int v23; // edi
  __int64 v24; // rax
  __int64 v25; // rcx
  __int16 v26; // di
  __int16 v27; // r14
  int v28; // ebx
  __int64 v29; // rax
  __int64 v30; // rcx
  __int16 v31; // di
  __int16 v32; // r14
  int v33; // ebx
  __int64 v34; // rax
  __int64 v35; // rcx
  __int16 v36; // di
  __int16 v37; // r14
  int v38; // ebx
  __int64 v39; // rax
  __int64 v40; // rcx
  __int16 v41; // di
  __int16 v42; // r14
  int v43; // ebx
  __int64 v44; // rax
  __int64 v45; // rcx
  __int16 v46; // di
  __int16 v47; // r14
  int v48; // ebx
  __int64 v49; // rax
  __int64 v50; // rcx
  int v51; // edi
  __int64 v52; // rax
  __int64 v53; // rcx
  int v54; // edi
  __int64 v55; // rax
  __int64 v56; // rcx
  int v57; // edi
  __int64 v58; // rax
  __int64 v59; // rcx
  int v60; // edi
  __int64 v61; // rax
  __int64 v62; // rcx
  char v63; // bl
  char v64; // al
  char v65; // dl
  char v66; // dl
  char v67; // dl
  char v68; // dl
  char v69; // al
  char v70; // bl
  char v71; // dl
  char v72; // dl
  char v73; // dl
  char v74; // dl
  char v75; // dl
  char v76; // dl
  char v77; // al
  char v78; // dl
  char v79; // dl
  _DWORD *v80; // rdi
  __int64 v81; // rcx
  _DWORD *v82; // rdi
  _DWORD *v83; // rdi
  _DWORD *v84; // rdi
  _DWORD *v85; // rdi
  __int64 v86; // rcx
  __int64 v87; // rax
  __int64 v88; // rcx
  __int64 v89; // [rsp+20h] [rbp-40h] BYREF
  __int64 v90; // [rsp+28h] [rbp-38h]
  char v91; // [rsp+30h] [rbp-30h] BYREF
  char v92; // [rsp+31h] [rbp-2Fh] BYREF
  char v93; // [rsp+32h] [rbp-2Eh] BYREF
  char v94; // [rsp+33h] [rbp-2Dh] BYREF
  char v95[4]; // [rsp+34h] [rbp-2Ch] BYREF
  __int64 v96; // [rsp+38h] [rbp-28h] BYREF
  __int64 v97; // [rsp+40h] [rbp-20h]
  __int64 v98; // [rsp+48h] [rbp-18h]
  _DWORD *v99; // [rsp+50h] [rbp-10h]
  __int64 v100; // [rsp+58h] [rbp-8h]

  v100 = -2;
  result = 0;
  if ( a2 <= 1131631442 )
  {
    switch ( a2 )
    {
      case 1130786883:
        v5 = *((_WORD *)a1 + 2);
        v6 = *((_WORD *)a1 + 3);
        v7 = *((char *)a1 + 15);
        v8 = sub_14083D4F0(a1) + 40;
        if ( v5 == -1 )
          v7 = 40;
        if ( v6 == -1 )
          v7 = 40;
        LODWORD(v97) = v7;
        v96 = v8;
        if ( &v96 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v9 = v96;
          v10 = v97;
          a3[1] = v97;
          *a3 = v9;
          v8 = sub_14083D4F0(v10) + 8;
          v97 = 0;
          v96 = v8;
        }
        goto LABEL_84;
      case 1130786884:
      case 1130786885:
      case 1130786887:
      case 1130786888:
      case 1130786889:
      case 1130786890:
      case 1130786891:
      case 1130786892:
      case 1130786893:
      case 1130786894:
      case 1130786895:
      case 1130786896:
      case 1130786897:
      case 1130786898:
      case 1130786899:
      case 1130786900:
      case 1130786901:
      case 1130786902:
      case 1130786903:
      case 1130786904:
      case 1130786905:
      case 1130786906:
      case 1130786907:
      case 1130786908:
      case 1130786909:
      case 1130786910:
      case 1130786911:
      case 1130786912:
      case 1130786913:
      case 1130786914:
      case 1130786916:
      case 1130786917:
      case 1130786919:
      case 1130786921:
      case 1130786922:
      case 1130786923:
      case 1130786924:
      case 1130786925:
      case 1130786926:
      case 1130786927:
      case 1130786928:
      case 1130786929:
        return result;
      case 1130786886:
        v31 = *((_WORD *)a1 + 2);
        v32 = *((_WORD *)a1 + 3);
        v33 = *((char *)a1 + 17);
        v8 = sub_14083D4F0(a1) + 40;
        if ( v31 == -1 )
          v33 = 10;
        if ( v32 == -1 )
          v33 = 10;
        LODWORD(v97) = v33;
        v96 = v8;
        if ( &v96 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v34 = v96;
          v35 = v97;
          a3[1] = v97;
          *a3 = v34;
          v8 = sub_14083D4F0(v35) + 8;
          v97 = 0;
          v96 = v8;
        }
        goto LABEL_84;
      case 1130786915:
        v36 = *((_WORD *)a1 + 2);
        v37 = *((_WORD *)a1 + 3);
        v38 = *((char *)a1 + 19);
        v8 = sub_14083D4F0(a1) + 40;
        if ( v36 == -1 )
          v38 = 20;
        if ( v37 == -1 )
          v38 = 20;
        LODWORD(v97) = v38;
        v96 = v8;
        if ( &v96 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v39 = v96;
          v40 = v97;
          a3[1] = v97;
          *a3 = v39;
          v8 = sub_14083D4F0(v40) + 8;
          v97 = 0;
          v96 = v8;
        }
        goto LABEL_84;
      case 1130786918:
        v41 = *((_WORD *)a1 + 2);
        v42 = *((_WORD *)a1 + 3);
        v43 = *((char *)a1 + 16);
        v8 = sub_14083D4F0(a1) + 40;
        if ( v41 == -1 )
          v43 = 20;
        if ( v42 == -1 )
          v43 = 20;
        LODWORD(v97) = v43;
        v96 = v8;
        if ( &v96 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v44 = v96;
          v45 = v97;
          a3[1] = v97;
          *a3 = v44;
          v8 = sub_14083D4F0(v45) + 8;
          v97 = 0;
          v96 = v8;
        }
        goto LABEL_84;
      case 1130786920:
        v46 = *((_WORD *)a1 + 2);
        v47 = *((_WORD *)a1 + 3);
        v48 = *((char *)a1 + 14);
        v8 = sub_14083D4F0(a1) + 40;
        if ( v46 == -1 )
          v48 = 10;
        if ( v47 == -1 )
          v48 = 10;
        LODWORD(v97) = v48;
        v96 = v8;
        if ( &v96 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v49 = v96;
          v50 = v97;
          a3[1] = v97;
          *a3 = v49;
          v8 = sub_14083D4F0(v50) + 8;
          v97 = 0;
          v96 = v8;
        }
        goto LABEL_84;
      case 1130786930:
        v26 = *((_WORD *)a1 + 2);
        v27 = *((_WORD *)a1 + 3);
        v28 = *((char *)a1 + 18);
        v8 = sub_14083D4F0(a1) + 40;
        if ( v26 == -1 )
          v28 = 0;
        if ( v27 == -1 )
          v28 = 0;
        LODWORD(v97) = v28;
        v96 = v8;
        if ( &v96 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v29 = v96;
          v30 = v97;
          a3[1] = v97;
          *a3 = v29;
          v8 = sub_14083D4F0(v30) + 8;
          v97 = 0;
          v96 = v8;
        }
        goto LABEL_84;
      default:
        if ( a2 != 1130779465 )
        {
          if ( a2 != 1131631430 )
            return result;
          v17 = *a1;
          v8 = sub_14083D4F0(a1) + 40;
          LODWORD(v97) = v17;
          v96 = v8;
          if ( &v96 != a3 )
          {
            (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v18 = v96;
            v19 = v97;
            a3[1] = v97;
            *a3 = v18;
            v8 = sub_14083D4F0(v19) + 8;
            v97 = 0;
            v96 = v8;
          }
          goto LABEL_84;
        }
        v63 = *((_BYTE *)a1 + 13);
        v64 = 4;
        v65 = 4;
        if ( v63 <= 18 )
        {
          if ( v63 >= 3 )
          {
            v65 = 3;
            if ( (unsigned __int8)v63 <= 0xEu )
              v65 = 2 - ((unsigned __int8)v63 < 6u);
          }
          else
          {
            v65 = 0;
          }
        }
        v95[0] = v65;
        v66 = *((_BYTE *)a1 + 9);
        if ( v66 > 18 )
          goto LABEL_97;
        if ( v66 < 3 )
          goto LABEL_92;
        v67 = 3 * v66;
        if ( *((_WORD *)a1 + 3) != 0xFFFF && *((_WORD *)a1 + 2) != 0xFFFF )
          v67 = *((_BYTE *)a1 + 15) + *((_BYTE *)a1 + 14) + v67 - *((_BYTE *)a1 + 19) - 30;
        if ( v67 <= 34 )
        {
          if ( v67 < -34 )
          {
LABEL_92:
            v64 = 0;
          }
          else
          {
            v64 = 3;
            if ( v67 <= 14 )
              v64 = 2 - (v67 < -14);
          }
        }
LABEL_97:
        v91 = v64;
        v68 = *((_BYTE *)a1 + 10);
        v69 = 4;
        v70 = 4;
        if ( v68 > 18 )
          goto LABEL_108;
        if ( v68 < 3 )
          goto LABEL_99;
        v71 = 3 * v68;
        if ( *((_WORD *)a1 + 3) == 0xFFFF || *((_WORD *)a1 + 2) == 0xFFFF )
        {
          v72 = v71 - 20;
        }
        else
        {
          v72 = *((_BYTE *)a1 + 16) + v71 - *((_BYTE *)a1 + 17) - 30;
          v70 = 4;
          if ( v72 > 34 )
            goto LABEL_108;
          if ( v72 < -34 )
          {
LABEL_99:
            v70 = 0;
            goto LABEL_108;
          }
        }
        v70 = 3;
        if ( v72 <= 14 )
          v70 = 2 - (v72 < -14);
LABEL_108:
        v92 = v70;
        v73 = *((_BYTE *)a1 + 12);
        if ( v73 > 18 )
          goto LABEL_116;
        if ( v73 < 3 )
          goto LABEL_110;
        v74 = 3 * v73;
        if ( *((_WORD *)a1 + 3) == 0xFFFF || *((_WORD *)a1 + 2) == 0xFFFF )
          v75 = v74 - 10;
        else
          v75 = *((_BYTE *)a1 + 19) + *((_BYTE *)a1 + 16) + v74 - (*((_BYTE *)a1 + 17) + *((_BYTE *)a1 + 14)) - 30;
        if ( v75 <= 34 )
        {
          if ( v75 < -34 )
          {
LABEL_110:
            v69 = 0;
            goto LABEL_116;
          }
          v69 = 3;
          if ( v75 <= 14 )
            v69 = 2 - (v75 < -14);
        }
LABEL_116:
        v94 = v69;
        v76 = *((_BYTE *)a1 + 8);
        v77 = 4;
        if ( v76 <= 18 )
        {
          if ( v76 >= 3 )
          {
            v78 = 3 * v76;
            if ( *((_WORD *)a1 + 3) == 0xFFFF || *((_WORD *)a1 + 2) == 0xFFFF )
              v79 = v78 - 10;
            else
              v79 = *((_BYTE *)a1 + 15) + *((_BYTE *)a1 + 14) + v78 - (*((_BYTE *)a1 + 19) + *((_BYTE *)a1 + 17)) - 30;
            if ( v79 > 34 )
              goto LABEL_124;
            if ( v79 >= -34 )
            {
              v77 = 3;
              if ( v79 <= 14 )
                v77 = 2 - (v79 < -14);
              goto LABEL_124;
            }
          }
          v77 = 0;
        }
LABEL_124:
        v93 = v77;
        sub_1412D5BA0(&v96);
        *(_DWORD *)(v98 + 12) &= ~2u;
        v99[3] &= ~2u;
        v80 = v99;
        (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v99 + 40LL))(v99, 0x1418BD3D9LL, 1);
        if ( v80[4] == 0 )
        {
          v82 = v99;
          (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v99 + 40LL))(v99, v95, 1);
          if ( v82[4] == 0 )
          {
            v83 = v99;
            (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v99 + 40LL))(v99, &v92, 1);
            if ( v83[4] == 0 )
            {
              v84 = v99;
              (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v99 + 40LL))(v99, &v91, 1);
              if ( v84[4] == 0 )
              {
                v85 = v99;
                (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v99 + 40LL))(v99, &v93, 1);
                if ( v85[4] == 0 )
                  (*(void (__fastcall **)(_DWORD *, char *, __int64))(*(_QWORD *)v99 + 40LL))(v99, &v94, 1);
              }
            }
          }
        }
        v90 = 0;
        v89 = sub_14083D4F0(v81) + 8;
        if ( dword_141B59E30 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                         + 4LL) )
        {
          sub_141750E08(&dword_141B59E30);
          if ( dword_141B59E30 == -1 )
          {
            sub_1408040C0(&qword_141B59E00);
            sub_141751048(sub_140804150);
            sub_141750EA0(&dword_141B59E30);
          }
        }
        sub_140804F40(&qword_141B59E00, &v89, &v96);
        sub_1412D68A0(&v96);
        v86 = *a3;
        if ( &v89 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v86 + 16LL))(v86, a3);
          v87 = v89;
          v88 = v90;
          a3[1] = v90;
          *a3 = v87;
          v86 = sub_14083D4F0(v88) + 8;
          v90 = 0;
          v89 = v86;
        }
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v86 + 16LL))(v86, &v89);
        return 1;
    }
  }
  if ( a2 > 1131638884 )
  {
    if ( a2 > 1131638899 )
    {
      if ( a2 == 1131638900 )
      {
        v60 = *((char *)a1 + 10);
        v8 = sub_14083D4F0(a1) + 40;
        LODWORD(v97) = v60;
        v96 = v8;
        if ( &v96 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v61 = v96;
          v62 = v97;
          a3[1] = v97;
          *a3 = v61;
          v8 = sub_14083D4F0(v62) + 8;
          v97 = 0;
          v96 = v8;
        }
      }
      else
      {
        if ( a2 != 1131639909 )
          return result;
        v23 = *((char *)a1 + 12);
        v8 = sub_14083D4F0(a1) + 40;
        LODWORD(v97) = v23;
        v96 = v8;
        if ( &v96 != a3 )
        {
          (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v24 = v96;
          v25 = v97;
          a3[1] = v97;
          *a3 = v24;
          v8 = sub_14083D4F0(v25) + 8;
          v97 = 0;
          v96 = v8;
        }
      }
    }
    else if ( a2 == 1131638885 )
    {
      v54 = *((char *)a1 + 13);
      v8 = sub_14083D4F0(a1) + 40;
      LODWORD(v97) = v54;
      v96 = v8;
      if ( &v96 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v55 = v96;
        v56 = v97;
        a3[1] = v97;
        *a3 = v55;
        v8 = sub_14083D4F0(v56) + 8;
        v97 = 0;
        v96 = v8;
      }
    }
    else
    {
      if ( a2 != 1131638899 )
        return result;
      v14 = *((char *)a1 + 9);
      v8 = sub_14083D4F0(a1) + 40;
      LODWORD(v97) = v14;
      v96 = v8;
      if ( &v96 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v15 = v96;
        v16 = v97;
        a3[1] = v97;
        *a3 = v15;
        v8 = sub_14083D4F0(v16) + 8;
        v97 = 0;
        v96 = v8;
      }
    }
  }
  else if ( a2 > 1131635045 )
  {
    if ( a2 == 1131635046 )
    {
      v57 = *((char *)a1 + 11);
      v8 = sub_14083D4F0(a1) + 40;
      LODWORD(v97) = v57;
      v96 = v8;
      if ( &v96 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v58 = v96;
        v59 = v97;
        a3[1] = v97;
        *a3 = v58;
        v8 = sub_14083D4F0(v59) + 8;
        v97 = 0;
        v96 = v8;
      }
    }
    else
    {
      if ( a2 != 1131637881 )
        return result;
      v20 = *((char *)a1 + 8);
      v8 = sub_14083D4F0(a1) + 40;
      LODWORD(v97) = v20;
      v96 = v8;
      if ( &v96 != a3 )
      {
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v21 = v96;
        v22 = v97;
        a3[1] = v97;
        *a3 = v21;
        v8 = sub_14083D4F0(v22) + 8;
        v97 = 0;
        v96 = v8;
      }
    }
  }
  else if ( a2 == 1131631443 )
  {
    v51 = *((__int16 *)a1 + 2);
    v8 = sub_14083D4F0(a1) + 40;
    LODWORD(v97) = v51;
    v96 = v8;
    if ( &v96 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v52 = v96;
      v53 = v97;
      a3[1] = v97;
      *a3 = v52;
      v8 = sub_14083D4F0(v53) + 8;
      v97 = 0;
      v96 = v8;
    }
  }
  else
  {
    if ( a2 != 1131631444 )
      return result;
    v11 = *((__int16 *)a1 + 3);
    v8 = sub_14083D4F0(a1) + 40;
    LODWORD(v97) = v11;
    v96 = v8;
    if ( &v96 != a3 )
    {
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
      v12 = v96;
      v13 = v97;
      a3[1] = v97;
      *a3 = v12;
      v8 = sub_14083D4F0(v13) + 8;
      v97 = 0;
      v96 = v8;
    }
  }
LABEL_84:
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v8 + 16LL))(v8, &v96);
  return 1;
}
