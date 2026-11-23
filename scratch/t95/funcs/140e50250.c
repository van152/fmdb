__int64 __fastcall sub_140E50250(__int64 a1)
{
  int v1; // ebp
  int v3; // ecx
  int v4; // r14d
  __int64 v5; // rcx
  bool v6; // zf
  __int64 v7; // rcx
  __int64 v8; // rbx
  __int64 v9; // rdx
  bool v10; // cf
  __int16 v11; // dx
  int v12; // edx
  int v13; // edx
  int v14; // eax
  int v15; // edx
  int v16; // ebx
  int v17; // edi
  __int64 v18; // rdx
  __int64 v19; // r8
  int v20; // r9d
  __int64 v21; // rax
  __int16 v22; // bx
  __int64 v23; // rdi
  __int64 v24; // rdi
  __int64 v25; // rcx
  __int64 v26; // rdx
  __int16 v27; // ax
  int v28; // eax
  int v29; // eax
  int v30; // ecx
  double v31; // xmm0_8
  __int64 v32; // rdx
  __int64 v33; // rdx
  int v34; // ecx
  double v35; // xmm0_8
  __int64 v36; // rdi
  __int64 *v37; // r11
  __int16 v38; // r10
  double v39; // xmm0_8
  double v40; // xmm0_8
  int v41; // edi
  int v42; // ebx
  int v43; // eax
  int v44; // ebp
  int v45; // edx
  int v46; // eax

  v3 = *(unsigned __int16 *)(a1 + 82);
  v4 = *(unsigned __int16 *)(a1 + 84);
  if ( (unsigned __int16)(v3 - 201) <= 0xFF37u )
  {
    if ( (unsigned __int16)(v4 - 1) > 0xC7u )
      goto LABEL_7;
    v5 = *(_QWORD *)(a1 + 32);
    if ( v5 == 0 )
      goto LABEL_7;
    v6 = *(_BYTE *)(v5 + 47) == 0;
    v7 = *(_QWORD *)(v5 + 48);
    v8 = 368;
    if ( v6 )
      v8 = 216;
    v9 = *(_QWORD *)(v7 + v8);
    LOWORD(v7) = *(_WORD *)(a1 + 84);
    if ( v9 != *(_QWORD *)(a1 + 48) )
    {
LABEL_7:
      LODWORD(v7) = *(_DWORD *)(a1 + 80);
      if ( (unsigned __int16)(v7 - 1) > 0xC7u )
      {
        v11 = *(_WORD *)(a1 + 86);
        if ( *(__int16 *)(a1 + 88) > -8 || (LOWORD(v7) = 80, v11 <= 100) )
        {
          LOWORD(v7) = 30;
          if ( (unsigned __int16)(v11 - 1) <= 0xC7u )
          {
            LOWORD(v7) = 12;
            if ( (unsigned __int16)v11 >= 0x4Cu )
              LOWORD(v7) = v11 - 25;
          }
        }
      }
      else
      {
        v10 = (unsigned __int16)v7 < 0xB4u;
        LOWORD(v7) = 170;
        if ( v10 )
          LOWORD(v7) = *(_DWORD *)(a1 + 80);
      }
    }
    LODWORD(v7) = (__int16)v7;
    if ( *(_QWORD *)(a1 + 32) == 0 )
      LODWORD(v7) = (int)((double)(__int16)v7 * MEMORY[0x141865B68]);
    v12 = 1;
    if ( (__int16)v7 >= 2 )
      v12 = v7;
    v3 = 200;
    if ( (unsigned __int16)v12 < 0xC8u )
      v3 = v12;
    *(_WORD *)(a1 + 82) = v3;
  }
  if ( (unsigned __int16)(v4 - 201) <= 0xFF37u )
  {
    v13 = 185;
    if ( (unsigned __int16)v3 < 0xBFu )
      v13 = (unsigned __int16)v3;
    v14 = 3;
    if ( (unsigned __int16)v3 >= 0xAu )
      v14 = v13;
    v15 = (int)((double)(__int16)v14 * MEMORY[0x141865B68]);
    if ( *(_QWORD *)(a1 + 32) != 0 )
      v15 = v14;
    v16 = 1;
    if ( (__int16)v15 >= 2 )
      v16 = v15;
    v4 = 200;
    if ( (unsigned __int16)v16 < 0xC8u )
      v4 = v16;
    *(_WORD *)(a1 + 84) = v4;
  }
  v17 = *(_DWORD *)(a1 + 80);
  v18 = (unsigned __int16)(v17 - 201);
  if ( (unsigned int)v18 < 0xFF38 )
  {
    v19 = *(unsigned __int8 *)(a1 + 100);
    v20 = 0;
    if ( (_BYTE)v19 != 0 && *(__int16 *)(a1 + 86) >= 81 )
    {
      v21 = (*(__int64 (__fastcall **)(__int64, __int64, __int64, _QWORD))(*(_QWORD *)a1 + 560LL))(a1, v18, v19, 0);
      v22 = 1;
      if ( v21 != 0 )
      {
        if ( (v23 = v21, (unsigned __int8)sub_140087030() != 0)
          && (*(_QWORD *)(a1 + 24) & 0x1000) != 0
          && *(_QWORD *)(v23 + 272) != 0
          || *(_QWORD *)(v23 + 264) != 0 )
        {
          v24 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)a1 + 560LL))(a1);
          if ( (unsigned __int8)sub_140087030() == 0
            || (*(_QWORD *)(a1 + 24) & 0x1000) == 0
            || (v25 = *(_QWORD *)(v24 + 272)) == 0 )
          {
            v25 = *(_QWORD *)(v24 + 264);
          }
          v26 = *(_QWORD *)(v25 + 24);
          v27 = 1500;
          if ( v26 != *(_QWORD *)(v25 + 32) && *(_QWORD *)v26 != 0 )
            v27 = *(_WORD *)(*(_QWORD *)v26 + 168LL);
          v22 = 1;
          if ( (unsigned __int16)(v27 + 499) >= 0x3E7u )
            v22 = v27 / 500;
        }
      }
      LODWORD(v19) = *(unsigned __int8 *)(a1 + 100);
      v28 = 30;
      if ( (unsigned int)v19 <= 0x4B )
      {
        v28 = 25;
        if ( (unsigned __int8)v19 <= 0x32u )
        {
          v28 = 20;
          if ( (unsigned __int8)v19 <= 0xFu )
          {
            v28 = 5;
            if ( (_BYTE)v19 != 1 )
              v28 = v19 + 5;
          }
        }
      }
      v29 = (int)((double)(v28 * v22) * MEMORY[0x141861B70]);
      if ( (__int16)v29 >= 21 )
        v29 = (int)((double)(unsigned __int16)(v29 - 20) * MEMORY[0x14186AAA0] + MEMORY[0x141861B50]);
      v30 = 50;
      if ( (__int16)v29 < 50 )
        v30 = v29;
      v20 = 2;
      if ( (__int16)v30 >= 3 )
        v20 = v30;
      v4 = *(unsigned __int16 *)(a1 + 84);
    }
    if ( (unsigned __int16)(v4 - 1) <= 0xC7u )
    {
      if ( (unsigned __int16)v4 >= 0x88u )
      {
        v31 = (double)(__int16)v4 * MEMORY[0x141865B68];
LABEL_91:
        v1 = (int)v31;
        goto LABEL_92;
      }
      if ( (unsigned __int16)v4 >= 0x6Fu )
      {
        v34 = (__int16)v4;
LABEL_82:
        v35 = (double)v34;
        goto LABEL_83;
      }
      LOWORD(v1) = 2;
      if ( (unsigned __int16)v4 >= 0x56u )
      {
        v34 = (__int16)v4;
LABEL_88:
        v31 = (double)v34 * MEMORY[0x14186AB28];
        goto LABEL_91;
      }
      goto LABEL_92;
    }
    LOWORD(v34) = *(_WORD *)(a1 + 82);
    if ( (unsigned __int16)(v34 - 1) > 0xC7u )
    {
      LOWORD(v34) = *(_WORD *)(a1 + 86);
      LOWORD(v1) = 5;
      if ( (unsigned __int16)(v34 - 1) > 0xC7u )
        goto LABEL_92;
      if ( (unsigned __int16)v34 >= 0x92u )
      {
        v34 = (__int16)v34;
        goto LABEL_82;
      }
      if ( (unsigned __int16)v34 >= 0x7Eu )
      {
        v34 = (__int16)v34;
        goto LABEL_88;
      }
      LOWORD(v1) = 2;
      if ( (unsigned __int16)v34 < 0x56u )
      {
LABEL_92:
        *(_WORD *)(a1 + 80) = v1;
        v32 = *(_QWORD *)(a1 + 32);
        if ( v32 == 0 && (unsigned __int16)v20 <= 0x13u )
        {
          v1 = (int)((double)(__int16)v1 * MEMORY[0x141865B68]);
          *(_WORD *)(a1 + 80) = v1;
        }
        v3 = *(unsigned __int16 *)(a1 + 82);
        LODWORD(v36) = 1;
        if ( (__int16)v4 >= 50 || (__int16)v3 >= 50 )
        {
          LODWORD(v36) = v1;
          if ( v32 != 0 )
          {
            if ( *(_BYTE *)(v32 + 47) != 0 )
              goto LABEL_108;
            v36 = *(_QWORD *)(v32 + 48);
            if ( v36 == 0 )
              goto LABEL_108;
            v37 = *(__int64 **)(v36 + 24);
            v38 = 1500;
            if ( v37 != *(__int64 **)(v36 + 32) )
            {
              v36 = *v37;
              if ( *v37 != 0 )
                v38 = *(_WORD *)(v36 + 168);
            }
            if ( v38 > 7749 || (__int16)v1 < 16 || (unsigned __int8)v19 > 1u )
            {
LABEL_108:
              LODWORD(v36) = v1;
            }
            else
            {
              LOWORD(v36) = 1;
              if ( v38 >= 3750 )
              {
                v39 = (double)(__int16)v1 + MEMORY[0x14187BD10];
                if ( (unsigned __int16)v38 > 0x1675u )
                  v40 = v39 * MEMORY[0x141764678];
                else
                  v40 = v39 * MEMORY[0x14186AB28];
                LODWORD(v36) = (int)(v40 + MEMORY[0x1417C5160]);
              }
            }
          }
        }
        v41 = v20 + v36;
        v42 = *(__int16 *)(a1 + 86);
        if ( v42 >= 141 && (__int16)v41 < (__int16)(int)((double)v42 * MEMORY[0x14187BD18]) )
          v41 += (int)((double)(v42 - (__int16)v41) * MEMORY[0x14186AB28]);
        v43 = *(unsigned __int16 *)(a1 + 82);
        if ( (__int16)v41 < (__int16)v3 )
          v43 = v41;
        if ( (__int16)v43 >= (__int16)v4 )
          v43 = v4;
        v44 = 1;
        if ( (__int16)v43 >= 2 )
          v44 = v43;
        v17 = 200;
        if ( (unsigned __int16)v44 < 0xC8u )
          v17 = v44;
        *(_WORD *)(a1 + 80) = v17;
        if ( v32 == 0 )
          goto LABEL_121;
        goto LABEL_68;
      }
    }
    else
    {
      LOWORD(v1) = 2;
      if ( (unsigned __int16)v34 < 0x28u )
        goto LABEL_92;
      if ( (unsigned __int16)v34 > 0x54u )
      {
        v35 = (double)(__int16)v34;
        if ( (unsigned __int16)v34 <= 0x86u )
        {
          v31 = v35 * MEMORY[0x14186AB28];
          goto LABEL_91;
        }
LABEL_83:
        v31 = v35 * MEMORY[0x14187BD08];
        goto LABEL_91;
      }
    }
    v31 = (double)(__int16)v34 * MEMORY[0x141871418];
    goto LABEL_91;
  }
  v32 = *(_QWORD *)(a1 + 32);
  if ( v32 == 0 )
  {
LABEL_121:
    if ( *(_BYTE *)(a1 + 101) != 4 )
    {
      v45 = 1;
      if ( (__int16)(*(_WORD *)(a1 + 86) - 5) >= 2 )
        v45 = *(unsigned __int16 *)(a1 + 86) - 5;
      v46 = 200;
      if ( (unsigned __int16)v45 < 0xC8u )
        v46 = v45;
      *(_WORD *)(a1 + 86) = v46;
      if ( (unsigned __int16)v46 <= 0x95u )
      {
        if ( (__int16)v46 < (__int16)v3 )
          v3 = v46;
        if ( (__int16)v17 >= (__int16)v3 )
          v17 = v3;
      }
    }
    goto LABEL_131;
  }
LABEL_68:
  if ( *(_BYTE *)(v32 + 47) != 0 || (v33 = *(_QWORD *)(v32 + 48)) == 0 || *(_QWORD *)(v33 + 216) == *(_QWORD *)(a1 + 48) )
LABEL_131:
    LOWORD(v4) = v3;
  *(_WORD *)(a1 + 82) = 50 * v3;
  *(_WORD *)(a1 + 84) = 50 * v4;
  *(_WORD *)(a1 + 80) = 50 * v17;
  return (unsigned int)(50 * v17);
}
